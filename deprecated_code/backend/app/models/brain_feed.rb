class BrainFeed
  include Mongoid::Document
	field :toshow, type: Boolean
  	field :type, type: String
	field :text, type: String
	field :media, type: Array
	field :source_text, type: String
	field :source_url, type: Hash
	field :hashtags, type: String
	index({hashtags: 'text'})
	field :created_at, type: DateTime
end
