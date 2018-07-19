# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests
import json
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from flask import Flask
from flask_restful import Resource, Api

google_api_key = 'AIzaSyCD1cJUYVkuzr6xDqz4fOpfIpA_rLwWUg0'
session = Session(server_token='pRiNDj8r51vfn7M4i770hMkU24WnCF4E_v2i0-nk')
uber_client = UberRidesClient(session)
app = Flask(__name__)
api = Api(app)

class GetEstimates(Resource):
    def get(self, start, end):
        start_coord, end_coord = getGoogleCoordinates(start, end)  
        #Make the uber request
        uber_pool, uber_x = getUberEstimate(start_coord, end_coord)     
        #Make the lyft request
        lyft_line, lyft_ = getLyftEstimate(start_coord, end_coord)
        
        return uber_pool, uber_x, lyft_line, lyft_

api.add_resource(GetEstimates, '/getestimates/<string:start>/<string:end>')

class GetCoordinates(Resource):
    def get(self, start, end):
        start_coord, end_coord = getGoogleCoordinates(start, end)  
        
        return start_coord, end_coord
    
api.add_resource(GetCoordinates, '/getcoordinates/<string:start>/<string:end>')

# Get coordinates
def getGoogleCoordinates(start, end):
    start_resp = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+start+'&key='+google_api_key)
    end_resp = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+end+'&key='+google_api_key)     
    start_json = json.loads(start_resp.text)
    end_json = json.loads(end_resp.text)
        
    start_coord = start_json['results'][0]['geometry']['location']
    end_coord = end_json['results'][0]['geometry']['location']
        
    return start_coord, end_coord

def getUberEstimate(start_coord, end_coord):
    response = uber_client.get_price_estimates(
        start_latitude= start_coord['lat'],
        start_longitude= start_coord['lng'],
        end_latitude= end_coord['lat'],
        end_longitude= end_coord['lng'],
        seat_count=1
    )
        
    uber_estimates = response.json.get('prices')
    uber_pool = uber_estimates[0]
    uber_x = uber_estimates[1]
    
    return uber_pool, uber_x

def getLyftEstimate(start_coord, end_coord):
    lyft_est_resp = requests.get('https://api.lyft.com/v1/cost?start_lat='
                                     +str(start_coord['lat'])+'&start_lng='+str(start_coord['lng'])
                                     +'&end_lat='+str(end_coord['lat'])+'&end_lng='+str(end_coord['lng']),
                                     headers = {'Authorization': 'bearer j3aL7xIFYTyWMTl1i2qaiyGdfaGxcyGQRHXthANJdqbUNXfBilOqmlHvNvm'
                                                +'OxVgb3DdwsrKktjeKWv5jdzevdjEMd+plS71xwy91iNhSQ+XmtXlXqY+22UA='})        
    lyft_estimates = json.loads(lyft_est_resp.text)['cost_estimates']
    lyft_line = lyft_estimates[1]
    lyft_ = lyft_estimates[2]
    
    return lyft_line, lyft_  
    
if __name__ == '__main__':
#    while(True):
#        #Start google map coordinates request
#        start = raw_input('Enter starting location... ').replace(' ', '+')
#        end = raw_input('Enter destination... ').replace(' ', '+')
#        
#        start_coord, end_coord = getGoogleCoordinates(start, end)
#        
#        #Make the uber request
#        uber_pool, uber_x = getUberEstimate(start_coord, end_coord)
#        
#        #Make the lyft request
#        lyft_line, lyft_ = getLyftEstimate(start_coord, end_coord)   
    
    app.run(debug=True)
        
        
        
