class MethodReferenceSerializer < ActiveModel::Serializer
  attributes :abstract, :declaration, :discussion, :method_type, :name, :class_name, :url

  def class_name
    object.class_reference.name
  end
end
