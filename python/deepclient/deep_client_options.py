from typing import Any

class DeepClientOptions:
    def __init__(self, gql_client: Any = None,
                 table: str = 'links',
                 links_select_returning: str = 'id type_id from_id to_id value',
                 values_select_returning: str = 'id link_id value',
                 selectors_select_returning: str = 'item_id selector_id',
                 files_select_returning: str = 'id link_id name mimeType',
                 default_select_name: str = 'SELECT'):
        self.gql_client = gql_client

        self.table = table;

        self.links_select_returning = links_select_returning
        self.select_returning = self.links_select_returning
        self.values_select_returning = values_select_returning
        self.selectors_select_returning = selectors_select_returning
        self.files_select_returning = files_select_returning
        
        self.default_select_name = default_select_name
