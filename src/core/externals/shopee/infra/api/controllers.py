from ninja import NinjaAPI, Router
from django.core.cache import cache
from typing import Dict, Any

from src.core.externals.shopee.connection import Connection
from src.core.externals.shopee.infra.api.dtos import (
    ListProductsOutput,
    ProductAffiliateInput,
    response_create_link_affiliate,
    response_list_products,
)
from src.core.externals.shopee.service.product_service import ProductServcie
from src.config import settings
from google.genai import Client
router = Router(tags=["Shopee"])


@router.get("/", response=response_list_products)
async def list_products(request: NinjaAPI) -> ListProductsOutput:
    try:
        cache_key = "shopee:list_products"
        
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return 200, cached_result
            
        product_service = ProductServcie(
            connection=Connection(),
            client= Client(api_key=settings.GEMINI_API_KEY)
        )
        result = product_service.list_products()
        
        cache.set(cache_key, result, timeout=86400)
        
        
        return 200, result
    except Exception as e:
        print(f"Error in list_products: {str(e)}")
        return 400, {"message": str(e)}


@router.post("/product", response=response_create_link_affiliate)
async def create_link_affiliate(request: NinjaAPI, input: ProductAffiliateInput) -> ListProductsOutput:
    try:
        product_service = ProductServcie(
            connection=Connection(),
            client= Client(api_key=settings.GEMINI_API_KEY)
        )
        result = product_service.create_link_affiliate_by_url(input.product_url)
        
        return 201, result
    except Exception as e:
        raise e
        return 400, {"message": str(e)}


@router.delete("/cache", response={200: Dict[str, Any]})
async def clear_cache(request: NinjaAPI) -> tuple[int, Dict[str, Any]]:
    """
    Clear the cache for Shopee products.
    """
    try:
        # Get all keys with the shopee prefix
        keys = cache.keys("shopee:*")
        
        if keys:
            # Delete all keys
            cache.delete_many(keys)
            return 200, {"message": f"Cache cleared successfully. {len(keys)} keys removed."}
        else:
            return 200, {"message": "No cache keys found to clear."}
    except Exception as e:
        print(f"Error clearing cache: {str(e)}")
        return 400, {"message": str(e)}