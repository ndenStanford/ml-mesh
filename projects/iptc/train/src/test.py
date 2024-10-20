filtered_value="arts, entertainment"

query = f"""SELECT iptc_id, CURRENT_TIMESTAMP AS event_timestamp 
            FROM "features"."pred_iptc_first_level" 
            WHERE topic_1 = '{filtered_value}' """

print(query)