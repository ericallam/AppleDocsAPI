class CreateMethodReferences < ActiveRecord::Migration
  def change
    create_table :method_references do |t|
      t.text :name
      t.text :abstract
      t.text :discussion
      t.text :declaration
      t.text :anchor
      t.string :method_type
      t.integer :class_reference_id

      t.timestamps
    end
  end
end
