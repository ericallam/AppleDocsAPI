require 'multi_json'

namespace :docs do
  
  desc 'Create docs'
  task :create => :environment do
    ClassReference.delete_all
    MethodReference.delete_all
    ConstantReference.delete_all

    file = File.open('lib/appledocs/reference.json')

    begin
      MultiJson.decode(file.read).each do |doc_item|
        cf = ClassReference.new
        cf.name = doc_item['class_name']
        cf.overview = doc_item['overview']
        cf.ref_type = doc_item['reference_type']
        cf.url = doc_item['url']
        cf.save!

        doc_item['instance_methods'].each do |im|
           mf = cf.method_references.build im
           mf.method_type = "instance"
           mf.save!
        end

        doc_item['class_methods'].each do |cm|
           mf = cf.method_references.build cm
           mf.method_type = "class"
           mf.save!
        end

        doc_item['properties'].each do |p|
           mf = cf.method_references.build p
           mf.method_type = "property"
           mf.save!
        end

        doc_item["constants"].each do |const|
          cof = cf.constant_references.build name: const
          cof.save!
        end
      end
    rescue Exception => e
      puts e.inspect
    end
  end
end

module Docs
  def self.convertDescription(text)
    parsed = Nokogiri::HTML.parse(text)
    stripped_text = parsed.text
    parsed.css('code').each do |code|
      stripped_text.gsub!(" #{code.text} ", " ``#{code.text}`` ")
    end
    stripped_text.strip
  end

  def self.addMethod(parent, method, type)
    Doc.create(
      name: method['name'],
      description: convertDescription(method['abstract']),
      url: "#{parent['url']}##{method['anchor']}",
      options: {
        reference_type: type,
        declaration: convertDescription(method['declaration']),
        discussion: method['discussion'],
        parent: parent.name
      }
    )
  end

  def self.parsedOptions(options)
    options.collect do |option|
      {
        name: option['name'],
        declaration: convertDescription(option['declaration']),
      }
    end
  end
end