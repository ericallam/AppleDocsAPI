class ClassReference < ActiveRecord::Base
  attr_accessible :name, :overview, :ref_type, :url

  has_many :method_references
  has_many :constant_references
end
