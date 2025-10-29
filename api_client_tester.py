#!/usr/bin/env python3
"""
API Client Tester
A simple script to test API endpoints with GET, POST, PUT, and DELETE methods.
"""

import json
import requests
from typing import Optional, Dict, Any


class APIClient:
    """A client for testing API endpoints."""
    
    def __init__(self, base_url: str):
        """
        Initialize the API client with a base URL.
        
        Args:
            base_url: The base URL of the API server (e.g., 'http://localhost:8000')
        """
        self.base_url = base_url.rstrip('/')
    
    def _print_response(self, response: requests.Response) -> None:
        """
        Print the response in a readable format.
        
        Args:
            response: The HTTP response object
        """
        print(f"\nStatus Code: {response.status_code}")
        print(f"URL: {response.url}")
        
        try:
            json_data = response.json()
            print("Response Body:")
            print(json.dumps(json_data, indent=2))
        except ValueError:
            print("Response Body (non-JSON):")
            print(response.text)
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Perform a GET request.
        
        Args:
            endpoint: The API endpoint (e.g., '/users' or '/users/123')
            params: Optional query parameters
            
        Returns:
            The response object
        """
        url = f"{self.base_url}{endpoint}"
        print(f"\n{'='*60}")
        print(f"GET Request to: {url}")
        if params:
            print(f"Parameters: {params}")
        
        response = requests.get(url, params=params)
        self._print_response(response)
        return response
    
    def post(self, endpoint: str, payload: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Perform a POST request.
        
        Args:
            endpoint: The API endpoint (e.g., '/users')
            payload: Optional JSON payload to send
            
        Returns:
            The response object
        """
        url = f"{self.base_url}{endpoint}"
        print(f"\n{'='*60}")
        print(f"POST Request to: {url}")
        if payload:
            print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, json=payload)
        self._print_response(response)
        return response
    
    def put(self, endpoint: str, payload: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Perform a PUT request.
        
        Args:
            endpoint: The API endpoint (e.g., '/users/123')
            payload: Optional JSON payload to send
            
        Returns:
            The response object
        """
        url = f"{self.base_url}{endpoint}"
        print(f"\n{'='*60}")
        print(f"PUT Request to: {url}")
        if payload:
            print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.put(url, json=payload)
        self._print_response(response)
        return response
    
    def delete(self, endpoint: str) -> requests.Response:
        """
        Perform a DELETE request.
        
        Args:
            endpoint: The API endpoint (e.g., '/users/123')
            
        Returns:
            The response object
        """
        url = f"{self.base_url}{endpoint}"
        print(f"\n{'='*60}")
        print(f"DELETE Request to: {url}")
        
        response = requests.delete(url)
        self._print_response(response)
        return response


if __name__ == '__main__':
    # Example usage of the API Client
    # Configure the base URL for your API server
    BASE_URL = 'https://jsonplaceholder.typicode.com'
    
    # Create an instance of the API client
    client = APIClient(BASE_URL)
    
    print("API Client Tester - Example Usage")
    print("=" * 60)
    
    # Example 1: GET request to retrieve a list of resources
    print("\nExample 1: GET request to fetch a user")
    client.get('/users/1')
    
    # Example 2: GET request with query parameters
    print("\nExample 2: GET request with query parameters")
    client.get('/posts', params={'userId': 1})
    
    # Example 3: POST request to create a new resource
    print("\nExample 3: POST request to create a new post")
    new_post = {
        'title': 'Test Post',
        'body': 'This is a test post created by the API client tester.',
        'userId': 1
    }
    client.post('/posts', payload=new_post)
    
    # Example 4: PUT request to update an existing resource
    print("\nExample 4: PUT request to update a post")
    updated_post = {
        'id': 1,
        'title': 'Updated Test Post',
        'body': 'This post has been updated.',
        'userId': 1
    }
    client.put('/posts/1', payload=updated_post)
    
    # Example 5: DELETE request to remove a resource
    print("\nExample 5: DELETE request to remove a post")
    client.delete('/posts/1')
    
    print("\n" + "=" * 60)
    print("API Client Tester - Examples Complete")
