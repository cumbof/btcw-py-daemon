import os, sqlite3, datetime, requests, json
from pybitcoin import BitcoinPrivateKey

db_schema_file_path = "./schema.sql";
db_file_path = "./database.db";

def initializeDB():
    db_is_new = not os.path.exists(db_file_path);
    if db_is_new:
        with sqlite3.connect(db_file_path) as conn:
            print 'Creating DB';
            with open(db_schema_file_path, 'rt') as f:
                schema = f.read();
                conn.executescript(schema);

def query_db(query, args=(), one=False):
    with sqlite3.connect(db_file_path) as conn:
        cursor = conn.cursor();
        cursor.execute(query, args);    
        rv = cursor.fetchall()
        cursor.close()
        return (rv[0] if rv else None) if one else rv

def store_keys_inf(table, private_key_hex, private_key_wif, public_key_hex, wallet_address, hash160, timestamp):
    query_str = """
                insert into {table_id} (private_key_hex, private_key_wif, public_key_hex, wallet_address, hash160, query_timestamp) 
                values (
                    '{private_key_hex_str}', 
                    '{private_key_wif_str}', 
                    '{public_key_hex_str}', 
                    '{wallet_address_str}', 
                    '{hash160_str}', 
                    '{timestamp_str}'
                );
                """.format(
                        table_id=table,
                        private_key_hex_str=private_key_hex, 
                        private_key_wif_str=private_key_wif, 
                        public_key_hex_str=public_key_hex, 
                        wallet_address_str=wallet_address,
                        hash160_str=hash160,
                        timestamp_str=timestamp
                    );
    query_db(query_str);

def query_blockchain(private_key_hex, private_key_wif, public_key_hex, wallet_address, hash160, timestamp, recursive_limit=5):
    try:
        r = requests.get("https://blockchain.info/address/"+str(wallet_address)+"?format=json");
        if r.status_code == 200:
            json_data = r.json();
            if json_data['final_balance'] > 0:
                print("timestamp: "+timestamp);
                print("private key hex: "+private_key_hex);
                print("private key wif: "+private_key_wif);
                print("public key hex: "+public_key_hex);
                print("wallet address: "+wallet_address);
                print("hash160: "+hash160);
                print("-----------------------------------------------");
                store_keys_inf("found", private_key_hex, private_key_wif, public_key_hex, wallet_address, hash160, timestamp);
        else:
            store_keys_inf("failed", private_key_hex, private_key_wif, public_key_hex, wallet_address, hash160, timestamp);
    except:
        if recursive_limit > 0:
            query_blockchain(private_key_hex, private_key_wif, public_key_hex, wallet_address, hash160, timestamp, recursive_limit-1);
        else:
            store_keys_inf("failed", private_key_hex, private_key_wif, public_key_hex, wallet_address, hash160, timestamp);

def daemon():
    while True:
        timestamp = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'));
        private_key = BitcoinPrivateKey();
        private_key_hex = str(private_key.to_hex());
        private_key_wif = str(private_key.to_wif());
        public_key = private_key.public_key();
        public_key_hex = str(public_key.to_hex());
        wallet_address = str(public_key.address());
        hash160 = str(public_key.hash160());
        query_blockchain(private_key_hex, private_key_wif, public_key_hex, wallet_address, hash160, timestamp);

if __name__ == '__main__':
    initializeDB();
    daemon();
