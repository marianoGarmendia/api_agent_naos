from pydantic import BaseModel, Field
from typing import Union
from typing import Optional
import requests
import os

from langchain_core.tools import tool
from langchain_core.tools import StructuredTool


class ShopifyOrdersInput(BaseModel):
    order_number: str = Field(description="Numero de orden de shopify, (debe empezar siempre con las letras: EN)")

class DropGoOrdersInput(BaseModel):    
    tracking_number: str = Field( description="Número de seguimiento de dropGo, (Debe empezar con las letras: DP)")


@tool("get_shopify_order_status", args_schema=ShopifyOrdersInput, return_direct=True)
def get_shopify_order_status(order_number:str) -> Union[dict, list]:
    """Utilizar para obtener la información de la orden de pedido de shopify que será entregado por dropGo"""

    if order_number:
        shopifyDomain= "naoskingdom.myshopify.com"
        accessToken =  os.getenv("ACCESS_TOKEN_NAOS")
        url = f'https://{shopifyDomain}/admin/api/2024-01/orders.json'
        response = requests.get(url, headers={'X-Shopify-Access-Token': accessToken, 'Content-Type': 'application/json'})
        dataShopify = response.json()
        def get_shipping_by_order(order_name: str, data: dict) -> list :
            order_found = []
        
            # Iterar sobre las órdenes en data['orders']
            for order in data.get('orders', []):
                
                if order.get('fulfillments'):
                    for fulfillment in order['fulfillments']:
                        if fulfillment.get('name') == f'{order_name}.1':
                       
                            order_found.append({
                                'order': f'{order_name}.1',
                                'tracking_number': fulfillment.get('tracking_number'),
                            })
            if not order_found:
                return [{"Error": "No se encontraron órdenes con el número de seguimiento proporcionado"}]

            return order_found
       
        orders_found = get_shipping_by_order(order_number, dataShopify)
        if orders_found[0].get("Error"):
            return orders_found
        else:
            for order in orders_found:
                 tracking_number = order.get('tracking_number')
                 url = f'https://dropgo-red-xrodn5waiq-uc.a.run.app/api/seguimiento?trackingNumber={tracking_number}'
                 response = requests.get(url)
                # Verifica si la solicitud fue exitosa (código de estado 200)
                 if response.status_code == 200:
                    # Procesa los datos JSON de la respuesta
                    shipping = response.json()
                   
                        
                    return  {
                   "número de orden": order_number,    
                    "estado": shipping['details'][-1]['action'],
                    "direccion": shipping['customer_address'],
                    "fecha_de_envío": shipping['details'][-1]['date'],
                   "nombre": shipping['buyer_first_name'] + " " + shipping['buyer_last_name'],
                    "enviado por": shipping['customer_envio'],
                    "Observaciones del cliente": shipping['courier_obs'],
                    "Última persona con el pedido": shipping['details'][-1]['user'],
                    }
                  
                 else:
                # Maneja el error si la solicitud no fue exitosa
                     return {f'Error: {response.status_code}, Mensaje: {response.text}'}
            
        
    else:
        return {"Error": "No se ha ingresado un número de orden"}
   

@tool("get_shopify_order_status_by_num_seguimiento", args_schema=DropGoOrdersInput, return_direct=True) 
def get_shopify_order_status_by_num_seguimiento(tracking_number:str) -> Union[dict, list]:
        """Utilizar para obtener la información de la orden de pedido directamente a dropGo por numero de seguimiento
            este numero debe empezar con las letras: DP.
            La informacion a devolver esta dentro de la propiedad details
        """

        if tracking_number:
            url = f'https://dropgo-red-xrodn5waiq-uc.a.run.app/api/seguimiento?trackingNumber={tracking_number}'
            response = requests.get(url)
            # Verifica si la solicitud fue exitosa (código de estado 200)
            if response.status_code == 200:
                # Procesa los datos JSON de la respuesta
                shipping = response.json()
               
                        
                return  {
                   "número de orden": tracking_number,    
                    "estado": shipping['details'][-1]['action'],
                    "direccion": shipping['customer_address'],
                    "fecha_de_envío": shipping['details'][-1]['date'],
                   "nombre": shipping['buyer_first_name'] + " " + shipping['buyer_last_name'],
                    "enviado por": shipping['customer_envio'],
                    "Observaciones del cliente": shipping['courier_obs'],
                    "Última persona con el pedido": shipping['details'][-1]['user'],
                    }
            else:
                # Maneja el error si la solicitud no fue exitosa
                return {f'Error: {response.status_code}, Mensaje: {response.text}'}
        else:
            return {"Error": "No se ha ingresado un número de seguimiento"}