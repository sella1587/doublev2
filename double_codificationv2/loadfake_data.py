import pandas as pd
import psycopg
import io
def insert_using_copy_with_psycopg2(csvfile, table_name):
    to_table = "table_name"
    with psycopg.connect(dbname="DoubleCodification", user="owndblcodif", password="owndblcodif", host="Srvdocker2", port=5433) as con:
        with con.cursor() as cur:
            with open(csvfile, "r") as f:
                with cur.copy(f"COPY {table_name} (uid,source,name,component_type,description,trade,function,lot,room,code_client_ouvrage,code_client_object,code_fournisseur,facteur_choc,degre_choc,avec_plots,avec_carlingage,creation_date,date_last_modified,archived_date) FROM STDIN WITH (FORMAT CSV, DELIMITER ',', HEADER)" ) as copy:
                    while data := f.read(100):
                        copy.write(data)
            con.commit()

insert_using_copy_with_psycopg2("fakedata.csv","q35.objects_from_cao")
