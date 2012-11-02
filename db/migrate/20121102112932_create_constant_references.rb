class CreateConstantReferences < ActiveRecord::Migration
  def change
    create_table :constant_references do |t|
      t.text :name
      t.integer :class_reference_id

      t.timestamps
    end
  end
end
