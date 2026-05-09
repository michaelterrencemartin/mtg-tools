# Tooling to interact with the AllPrices.json file from the MTGJSON project
# Author: michael.terrence.martin@gmail.com
# 2026-05-08
import os
import json

from pprint import pprint


class MTGJSON_Parser:
    ALL_PRINTINGS_FILE = 'AllPrintings.json'
    ALL_PRICES_FILE = 'AllPricesToday.json'
    
    _printings_data = None
    _prices_data = None


    def __init__(self) -> None:
        """
        Handles opening the required files
        
        @raises: ValueError
        @return: None
        @author: michael.terrence.martin@gmail.com
        """
            
        self._check_files()
        self._populate()
        
    
    def _check_files(self) -> None:
        """
        Small wrapper for checking all files involved
        
        @return None
        @author michael.terrence.martin@gmail.com
        """
        
        self._check_file(self.ALL_PRINTINGS_FILE)
        self._check_file(self.ALL_PRICES_FILE)

    
    def _check_file(self, file: str) -> None:
        """
        Accepts a required file (str) paremeter and verifies that the file exists
        
        @raises: ValueError
        @return: None
        @author: michael.terrence.martin@gmail.com
        """
    
        if not file:
            raise ValueError('file parameter may not be empty!')
            
        if not os.path.exists(file):
            raise ValueError(f'file {file} not found!')
        

    def _populate(self) -> None:
        """
        Function to load JSON data from the file provided, if not already loaded
        
        @return: None
        @author michael.terrence.martin@gmail.com
        """
    
        # Load Printings Data
        if not self._printings_data:
            print('Loading Master Card Data...')
            with open(self.ALL_PRINTINGS_FILE, 'r', encoding='utf-8') as file:
                self._printings_data = json.load(file)
        
        if not self._prices_data:
            print('Loading Master Pricing Data...')
            with open(self.ALL_PRICES_FILE, 'r', encoding='utf-8') as file:
                self._prices_data = json.load(file)
            

    def dump_cards(
        self,
        cardname: str = None, 
        setcode: str = None, 
        language: str = None,
        limit: int = None
    ) -> list:
        """
        Dumps a number of or all cards matching the optional name, set, and language provided
        
        @param: cardname (str)
        @param: setcode (str)
        @param: language (str)
        @param: limit (int; default: 1; all: 0)
        @return: None
        @author michael.terrence.martin@gmail.com
        """

        if limit is None:
            limit = 1
            
        print(f'Dumping {limit if limit else 'all'} matching card(s)...')
        
        self._populate()
        
        count = 0
        results = []
            
        for setkey, setdata in self._printings_data.get('data').items():
        
            if limit and count >= limit:
                break
            
            if (setcode and setcode.lower() == setkey.lower()) or not setcode:

                cards = setdata.get('cards', [])
                
                for card in cards:
                
                    actual_name = card.get('faceName') if card.get('faceName') else card.get('name')
                    
                    if (cardname and cardname.lower() == actual_name.lower()) or not cardname:
                        
                        if (language and language.lower() == card.get('language').lower()) or not language:
                        
                            results.append(card)
                            
                            pprint(card)
                            count += 1
                            
                            if limit and count >= limit:
                                break
        print(' Finished ')
        return results


    def get_pricing(self, card: str | dict) -> dict:
        """
        Expects a card dict from the all printings data or a card UUID str
        
        @param card (str | dict)
        @return dict
        @raises ValueError
        @author michael.terrence.martin@gmail.com
        """
        
        card_uuid = None
        
        if type(card) is dict:
            card_uuid = card.get('uuid')
        else:
            card_uuid = card
            
        if not card:
            raise ValueError('card must be printings dictionary or a uuid string')

        return self._prices_data.get('data').get(card_uuid, {}).get('paper', {})

