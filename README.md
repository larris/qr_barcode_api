docker build -t qr_barcode .
docker run -it -p 80:5000 qr_barcode

docker build -t qr_barcode . & docker run -it -p 80:5000 qr_barcode