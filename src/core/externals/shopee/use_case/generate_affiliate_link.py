from typing import Optional

from src.core.externals.shopee.auth import ShopeeBaseAuth


class UcGenerateAffiliateLink(ShopeeBaseAuth):


    def execute(self, product_url: str) -> Optional[str]:
        """
        Generate a short affiliate link for a product URL.
        
        Args:
            product_url (str): The Shopee product URL
            
        Returns:
            Optional[str]: The generated short affiliate link
        """
        try:
            query = f'''mutation{{
                generateShortLink(input:{{
                    originUrl:"{product_url}",
                    subIds:["s1","s2","s3","s4","s5"]
                }}){{
                    shortLink
                }}
            }}'''
            
            response = self._make_request(query)
            return response.get('data', {}).get('generateShortLink', {}).get('shortLink', product_url)
            
        except Exception as e:
            print(f"Error generating affiliate link: {e}")
            return None

