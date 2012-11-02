AppleDocs::Application.routes.draw do
  get "api" => 'api#index'
  get "search" => 'api#search'
end
