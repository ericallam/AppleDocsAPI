from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from appledocs.items import ReferenceProperty, ReferenceClass, ReferenceClassMethod, ReferenceInstanceMethod, ReferenceConstantList

# Run this with

# The result of running that will give you a json file.  The json will be an array, and each item
# corresponds to a class (e.g. UIView) that is a json object.  Each class has these members:
#
#   :instance_methods: 
#   :class_methods:
#   :properties:
#   :reference_type:
#   :class_name:
#   :overview:
#   :url:
#   :constants:
#
# Description of each member:
#
# :instance_methods: is an Array of objects, each one representing a instance method belonging to the class/protocol. Each object has these members:
#
#   :name: String [the name of the method]
#   :abstract: String [a one sentence description of the method]
#   :discussion: String [a paragraph or two about the method]
#   :declaration: String [what the method definition looks like in code]
#   :anchor: String [allows you to construct a link right to this method]
#
# :class_methods: and :properties: have basically the same structure as :instance_methods:
#
# :class_name: is the name of the class/protocol
# :reference_type: is either 'Class' or 'Protocol'
# :overview: a String that contains a paragraph or so of discussion about the class/protocol
# :url: a String that contains a URL to the documentation page on Apple
#
# :constants: is an Array of strings, that list all the constants defined in that class/protocol. 

class BaseReferenceSpider(CrawlSpider):
    start_urls = ['https://developer.apple.com/library/ios/sitemap.php']

    def get_contents(self, selector, xpath):
      return ''.join(selector.select(xpath + '/child::node()').extract())

    def parse_constants(self, response):
      hxs = HtmlXPathSelector(response)
      constant_list = ReferenceConstantList()
      constant_list['constants'] = hxs.select('//code[@class="jump constantName"]/text()').extract()
      return constant_list

    def parse_reference(self, response):
      hxs = HtmlXPathSelector(response)
      reference_class = ReferenceClass()
      reference_class['constants'] = hxs.select('//code[@class="jump constantName"]/text()').extract()
      reference_class['url'] = response.url
      

      name = hxs.select('//*[@id="pageTitle"]/text()')
      if len(name) > 0:
        full_name = name.extract()[0]
        
        if "Protocol" in full_name:
          reference_class['reference_type'] = 'Protocol'
          reference_class['overview'] = self.get_contents(hxs, '//*[@id="contents"]/p[@class="abstract"]')
        else:
          reference_class['overview'] = self.get_contents(hxs, '//div[@id="Overview_section"]/p[@class="abstract"]')
          reference_class['reference_type'] = 'Class'

        reference_class['class_name'] = name.re('^\w*')[0]

      reference_class['properties'] = []
      reference_class['class_methods'] = []
      reference_class['instance_methods'] = []

      # properties
      properties = hxs.select('//div[@class="api propertyObjC"]')
      
      for prop in properties:
        property_item = ReferenceProperty()
        property_item['name'] = prop.select('h3[@class="jump propertyObjC method_property"]/text()').extract()[0]
        property_item['discussion'] = self.get_contents(prop, 'div[@class="api discussion"]/p')
        property_item['declaration'] = self.get_contents(prop, 'div[@class="declaration"]')
        property_item['abstract'] = self.get_contents(prop, 'p[@class="abstract"]')
        property_item['anchor'] = prop.select('a[contains(@name, "apple_ref/occ")][1]/@name').extract()[0]

        reference_class['properties'].append(property_item)

      class_methods = hxs.select('//div[@class="api classMethod"]')

      for cm in class_methods:
        cm_item = ReferenceClassMethod()

        cm_item['name'] = cm.select('h3[@class="jump classMethod"]/text()').extract()[0]
        cm_item['abstract'] = self.get_contents(cm, 'p[@class="abstract"]')
        cm_item['declaration'] = self.get_contents(cm, 'div[@class="declaration"]')
        cm_item['discussion'] = self.get_contents(cm, 'div[@class="api discussion"]/p')
        cm_item['anchor'] = cm.select('a[contains(@name, "apple_ref/occ")]/@name').extract()[0]

        reference_class['class_methods'].append(cm_item)

      instance_methods = hxs.select('//div[@class="api instanceMethod"]')

      for im in instance_methods:
        im_item = ReferenceInstanceMethod()

        im_item['name'] = im.select('h3[@class="jump instanceMethod"]/text()').extract()[0]
        im_item['abstract'] = self.get_contents(im, 'p[@class="abstract"]')
        im_item['declaration'] = self.get_contents(im, 'div[@class="declaration"]')
        im_item['discussion'] = self.get_contents(im, 'div[@class="api discussion"]/p')
        im_item['anchor'] = im.select('a[contains(@name, "apple_ref/occ")]/@name').extract()[0]

        reference_class['instance_methods'].append(im_item)

      return reference_class

class FoundationSpider(BaseReferenceSpider):
  name = 'foundation'
  rules = [
    Rule(SgmlLinkExtractor(allow=('/Foundation_Constants/', ), ), callback='parse_constants'),
    Rule(SgmlLinkExtractor(allow=('/Cocoa\/Reference\/Foundation\/Classes|Protocols/', ), ), callback='parse_reference'),
  ]

class ReferenceSpider(BaseReferenceSpider):
  name = 'reference'
  rules = [
    Rule(SgmlLinkExtractor(allow=('/ios\/documentation\/.*Reference.*(Class|Protocol)/', ), ), callback='parse_reference')
  ]