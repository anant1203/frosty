class CancelQuery:
    def __init__(self,session,session_id,query_id):
        self.session=session
        self.session_id=session_id
        self.query_id=query_id
    
    def cancel_query(self):
        self.session.sql(f"SELECT SYSTEM$CANCEL_QUERY('{self.query_id})")

    def cancel_all_queries(self):
        self.session.sql(f"SELECT SYSTEM$CANCEL_ALL_QUERIES({self.session_id})")
