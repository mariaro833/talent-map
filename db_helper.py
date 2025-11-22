from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

class DatabaseHelper:
    def __init__(self):
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://admin:password123@localhost:27017/talent_map?authSource=admin')
        
        try:
            self.client = MongoClient(mongo_uri)
            self.client.admin.command('ping')
            print("✓ Successfully connected to MongoDB!")
            
            self.db = self.client['talent_map']
            self.companies = self.db['companies']
            
        except ConnectionFailure as e:
            print(f"✗ Failed to connect to MongoDB: {e}")
            raise
    
    def insert_company(self, company_data):
        return self.companies.insert_one(company_data)
    
    def insert_companies(self, companies_list):
        if companies_list:
            return self.companies.insert_many(companies_list)
        return None
    
    def find_companies(self, query={}):
        return list(self.companies.find(query))
    
    def get_all_companies(self):
        return list(self.companies.find())
    
    def close_connection(self):
        self.client.close()
