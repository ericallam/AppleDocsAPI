class MethodReferenceSerializer < ActiveModel::Serializer
  attributes :abstract, :anchor, :declaration, :discussion, :method_type, :name, :class_name

  def class_name
    object.class_reference.name
  end
end
