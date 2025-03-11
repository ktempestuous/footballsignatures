import scrapy 
import os
from footballsignatures.items import FootballsignaturesItem

#create spider and define starting URL
class FootballsignatureSpider(scrapy.Spider):
	name = "footballsignature"
	allowed_domains = ["icons.com"]
	start_urls = ["https://www.icons.com/players/a-k.html"]

	# initialise
	def __init__(self, *args, **kwargs):
		super(FootballsignatureSpider, self).__init__(*args, **kwargs)
		
		# define output file 
		self.output_file = "output_file.json" 

		# delete output file if already exists 
		if os.path.exists(self.output_file):
			os.remove(self.output_file)
			self.log(f"Deleted previous output file: {self.output_file}")

	# parse website showing all players to identify those with surnames A-C 
	def parse(self,response):
		for footballer in response.css("li.item.product.product-item"):
			player_url = footballer.css("a::attr(href)").get() # url of each player's products 
			player_slug = footballer.css("a::attr(title)").get()
			player_slug =  player_slug.replace("View all ","")
			player_name =  player_slug.replace(" signed memorabilia","") #full player name 
			name_parts = player_name.split() # split to access first, last names etc.
			
			# create instance 
			item = FootballsignaturesItem()
			item["first_name"] = name_parts[0]
			item["last_name"] = name_parts[-1]
			item["full_name"] = player_name
			item["url"] = player_url

			if len(name_parts)>2: # deal with case of De as second last word but which is the beginning of the surname 
				second_last_name = name_parts[-2]
			else:
				second_last_name = ""

			# Check if "De" not in name and if surname begins with A, B or C. Account for special characters here.  
			if second_last_name != "De" and item["last_name"][0].upper() in ["A","\u00c1","B","C"]: 
		
				# apply filter to player URL to find the most expensive signed item for each player 
				price_descending = "&product_list_order=price_desc"
				filtered_url = f"{player_url}?player_names={player_name.replace(" ","+").replace("Á","A").replace("á","a")}{price_descending}"
		
				yield response.follow(filtered_url, callback=self.parse_player, meta={"item":item}) # follow URL to player's filtered product page 

	# obtain price of most expensive item of each player and follow to the URL of this item 
	def parse_player(self,response):
		item = response.meta["item"] 
		products = response.css("div.products.wrapper.mode-grid.products-grid")
		# check if any products are listed on the page
		if not products:
			self.log("No products found on this page")
			return 
		# extract price from most expensive item. In case of multiple items costing the maximimum amount, selects left most on page  
		price = products.css("span.price::text").get()
		item["price"] = price 
		# extract the URL of this most expensive item 
		first_product_url = products.css("a.inline-block.leading-relaxed.text-xxs.md\\:text-sm::attr(href)").get()
		yield response.follow(first_product_url,callback=self.parse_product, meta = {"item":item}) # follow URL to most expensive item 

	# obtain information of the most expensive item
	def parse_product(self, response):
		item = response.meta["item"]
		
		# extract title 
		title = response.css("span.base::text").get()
		if title:
			title = title.strip()
		else:
			title = "Not found"   # if there is no data for any category, "Not found" shown
		item["title"] = title

		#extract availability 
		availability = response.css('p[title="Availability"] span::text').get()
		if availability:
			availability = availability.strip()
		else:
			availability = "Not found"
		
		item["availability"] = availability 

		# extract size 
		size = response.css('td[data-th="Presentation size"]::text').get()
		if size:
			size = size.strip()
		else:
			size = "Not found"
		
		item["size"] = size 

		# extract product type 
		product_type = response.css('td[data-th="Product type(s)"]::text').get()
		
		if product_type:
			product_type = product_type.strip()
		else:
			product_type = "not found"
			
		item["product_type"] = product_type

		# extract presentation type 
		pres_type = response.css('td[data-th="Presentation type"]::text').get()
		
		if pres_type:
			pres_type = pres_type.strip()
		else:
			pres_type = "not found"
			
		item["presentation"] = pres_type

		if pres_type.lower() == "framed": # dispatch times depends on whether item is framed or not framed. Extract information from paragraphs. 
			dispatch_info = response.css('li:contains("Framed items take between")::text').get()
			dispatch_info = dispatch_info.replace("Framed items take between ","")
			dispatch_time = dispatch_info.replace(" to perfect and dispatch, after which delivery depends on where in the world we're sending your order to. Check out our full breakdown of estimated delivery times on our ","")

		else:
			dispatch_info = response.css('li:contains("We ship to almost all countries worldwide and aim to dispatch")::text').get()
			dispatch_time = dispatch_info.replace("We ship to almost all countries worldwide and aim to dispatch your orders within ","")

		item["dispatch_time"] = dispatch_time 

		yield item 

		

						
