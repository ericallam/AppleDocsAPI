class ClassReferenceSerializer < ActiveModel::Serializer
  attributes :name, :overview, :url, :type
  has_many :method_references

  def type
    object.ref_type
  end
end
