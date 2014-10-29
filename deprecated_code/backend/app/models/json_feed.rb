class JsonFeed
  include Mongoid::Document
  	field :type, type: String
	field :text, type: String
	field :media, type: Array
	field :mediamap, type: Array
	field :keywords, type: Array
	field :source_text, type: String
	field :source_url, type: Hash
	field :created_at, type: DateTime #private
	field :hashtags, type: String #private
	field :nodes, type: Array #private
	field :factors, type: Array #private
end
