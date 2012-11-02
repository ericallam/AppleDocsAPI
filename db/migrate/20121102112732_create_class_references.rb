class CreateClassReferences < ActiveRecord::Migration
  def change
    create_table :class_references do |t|
      t.string :ref_type
      t.text :name
      t.text :overview
      t.text :url

      t.timestamps
    end
  end
end
