require 'time'
class WebserverController < ApplicationController
  
  #http_basic_authenticate_with :name => "ashesh", :password => "123"
  skip_before_filter :verify_authenticity_token # we do not need devise authentication here


  def index
  end

  def json_feed_server
  	@feed = JsonFeed.new(feed_params)
	@feed.created_at = Time.now
	respond_to do |format|
		if @feed.save
			format.xml { render xml: @feed, status: :created }
			format.json { render json: @feed, status: :created }
		else
			format.json { render json: @feed.errors, status: :unprocessable_entity }
			format.xml { render xml: @feed.errors, status: :unprocessable_entity }
		end
	end

	# Writing to Brain Feed table for rendering latest brain feeds	
	viewer_feed_attribute = {:toshow => 1, :type => @feed.type, :text => @feed.text, :media => @feed.media, :source_text => @feed.source_text, :source_url => @feed.source_url, :created_at => @feed.created_at, :hashtags => @feed.hashtags}
	@viewer_feed = BrainFeed.new(viewer_feed_attribute)
	@viewer_feed.save
  end

  # Return feeds created after datetime. Input time should be in ISO string format. It is them parsed to UTC format
  def return_feeds_since
	time_since = Time.parse(params[:datetime])
	@feeds_since_time = BrainFeed.where(:toshow => 1).where(:created_at.gte => time_since).desc(:created_at)
 	respond_to do |format|
		format.xml { render xml: @feeds_since_time, status: :created }
		format.json { render json: @feeds_since_time, status:created }
	end
  end

  # Returns k most recent feeds from BrainFeed table.
  def return_top_k_feeds
  	top_k = params[:k].to_i
	@top_k_feeds = BrainFeed.where(:toshow => 1).desc(:created_at).take(top_k)
        #@data = {:callback => top_k_feeds}


	respond_to do |format|
		if params[:callback]
                	format.js {render :json =>  @top_k_feeds, :callback => params[:callback]}
		else
			format.json { render json: @top_k_feeds }
		end
		format.xml { render xml: @top_k_feeds }

	end
  end

  def feed_params
  	params.require(:feed).permit(:type,:text,:media => [])
  end
end
