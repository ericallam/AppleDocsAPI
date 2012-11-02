class MethodReference < ActiveRecord::Base
  attr_accessible :abstract, :anchor, :declaration, :discussion, :method_type, :name
  belongs_to :class_reference
end
