class ApiController < ApplicationController
  def index
    @class_reference = ClassReference.find_by_name params[:name]
    render json: @class_reference
  end

  def search
    @method_references = MethodReference.fuzzy_search name: params[:name]
    render json: @method_references
  end
end
