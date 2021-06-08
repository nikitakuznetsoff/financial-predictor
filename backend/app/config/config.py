class Config:
    CLIENT_ENDPOINT = "http://localhost:8080"
    
    POSTGRES_DBNAME = "finpred"
    POSTGRES_USERNAME = "nikita"
    POSTGRES_PASSWORD = "qwerty"
    POSTGRES_HOST = "localhost"
    POSTGRES_PORT = 5432

    SECRET_KEY = "my_super_secret_key"

    MONGO_DBNAME = "finPredictor"
    MONGO_USERNAME = "readWriteUser"
    MONGO_PASSWORD = "qwerty"
    MONGO_HOST = "localhost"
    MONGO_PORT = 27017


class HerokuConfig:
    CLIENT_ENDPOINT = "https://financial-pred.herokuapp.com/"
    
    POSTGRES_DBNAME = "d8i13q3pfpd7n6"
    POSTGRES_USERNAME = "hchvvefpfdsqgg"
    POSTGRES_PASSWORD = "cf195879baff908df4f1fba645bf307589db7363058e31ce23ab10074282afaa"
    POSTGRES_HOST = "ec2-63-34-97-163.eu-west-1.compute.amazonaws.com"
    POSTGRES_PORT = 5432

    SECRET_KEY = "my_super_secret_key"

    MONGO_DBNAME = "finpred"
    MONGO_USERNAME = "testUser"
    MONGO_PASSWORD = "qwdPZCqklg1vRXEk"
    MONGO_HOST = "cluster0.zi8rm.mongodb.net"
    MONGO_PORT = 27017