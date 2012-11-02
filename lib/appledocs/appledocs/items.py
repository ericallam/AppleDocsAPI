# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ReferenceConstantList(Item):
  constants = Field()

class ReferenceClass(Item):
  url = Field()
  reference_type = Field()
  overview = Field()
  constants = Field()
  class_name = Field()
  properties = Field()
  class_methods = Field()
  instance_methods = Field()

class ReferenceProperty(Item):
  name = Field()
  discussion = Field()
  declaration = Field()
  abstract = Field()
  anchor = Field()

class ReferenceClassMethod(Item):
  name = Field()
  abstract = Field()
  declaration = Field()
  discussion = Field()
  anchor = Field()

class ReferenceInstanceMethod(Item):
  name = Field()
  abstract = Field()
  declaration = Field()
  discussion = Field()
  anchor = Field()

