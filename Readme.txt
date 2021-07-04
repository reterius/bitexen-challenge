KURULUM ADIMLARI:

1) Projeyi repodan çekiniz
2) Proje klasörü içine giriniz
3) docker-compose up -d
4) Datayı bitexen apisinden alıp db ye taşıyan conteyner loglarını izlemek için: docker logs -f --tail=100  bitexen-challenge_beat_move_data_to_db_1
5) Db ye alınan datalardan gerekli istatistikleri hesaplayan conteyner loglarını izlemek için:   docker logs -f --tail=100  bitexen-challenge_beat_calculate_statistics_1




REST APİ:

Rest api dökümantasyonu: https://documenter.getpostman.com/view/5458897/Tzm2KJYp

Örn request;

Periyodu günlük olan ve min_price bilgisi taşıyan istatistik datalarını listelemek için: stats?stat_period=daily&stat_type=min_price&page=1&per_page=100
Periyodu günlük olan ve max_price bilgisi taşıyan istatistik datalarını listelemek için: stats?stat_period=daily&stat_type=max_price&page=1&per_page=100
Periyodu günlük olan ve average_price bilgisi taşıyan istatistik datalarını listelemek için: stats?stat_period=daily&stat_type=average_price&page=1&per_page=100
Periyodu günlük olan ve total_volume bilgisi taşıyan istatistik datalarını listelemek için: stats?stat_period=daily&stat_type=total_volume&page=1&per_page=100

Periyodu haftalık olan ve min_price bilgisi taşıyan istatistik datalarını listelemek için: stats?stat_period=weekly&stat_type=min_price&page=1&per_page=100
Periyodu haftalık olan ve max_price bilgisi taşıyan istatistik datalarını listelemek için: stats?stat_period=weekly&stat_type=max_price&page=1&per_page=100
Periyodu haftalık olan ve average_price bilgisi taşıyan istatistik datalarını listelemek için: stats?stat_period=weekly&stat_type=average_price&page=1&per_page=100
Periyodu haftalık olan ve total_volume bilgisi taşıyan istatistik datalarını listelemek için: stats?stat_period=weekly&stat_type=total_volume&page=1&per_page=100

Periyodu aylık olan ve min_price bilgisi taşıyan istatistik datalarını listelemek için: stats?stat_period=monthly&stat_type=min_price&page=1&per_page=100
Periyodu aylık olan ve max_price bilgisi taşıyan istatistik datalarını listelemek için: stats?stat_period=monthly&stat_type=max_price&page=1&per_page=100
Periyodu aylık olan ve average_price bilgisi taşıyan istatistik datalarını listelemek için: stats?stat_period=monthly&stat_type=average_price&page=1&per_page=100
Periyodu aylık olan ve total_volume bilgisi taşıyan istatistik datalarını listelemek için: stats?stat_period=monthly&stat_type=total_volume&page=1&per_page=100


Reuest parametreleri:

stat_period alabileceği değerler :

- daily (Günlük istatistik dataları için)
- weekly (Haftalık istatistik dataları için)
- monthly (Aylık istatistik dataları için)

stat_type alabileceği değerler :

- min_price
- max_price
- average_price
- total_volume



page (Gidilecek sayfa)
per_page (Sayfada bulunacak toplam kayıt sayısı)

######################################################

Response parametreleri:

İstediğiniz istatistik satırının hesaplanmış değeri tüm tipteki istatistikler için "quantity" adlı field'dır.
min_price, max_price, average_price ve total_volume tipindeki tüm istatistikler için istatistiğin hesaplanmış değeri hesaplandıktan sonra
"quantity" adlı field'a yazılır,


{
  "code": null,
  "data": {
    "items": [
      {
        "_id": "60e18af0fc92e60041e4a15c",
        "date_key": "2021|7|26|4",
        "day": 4,
        "last_calculated_date": "2021-07-04 15:07:26.435000",
        "month": 7,
        "quantity": 302989,  (Nihai olarak ilgili istatistiğin hesaplanmış datası buraya yazılır)
        "stat_period": "daily",
        "stat_type": "min_price",
        "total_amount_count": 0,
        "week": 26, (Kaçıncı hafta olduğu bilgisi)
        "year": 2021
      }
    ],
    "page": 1,
    "pages": 1,
    "per_page": 100,
    "total": 1
  },
  "description": null,
  "message": null,
  "pagination": null,
  "status": 200,
  "version": 1
}


FLOWER MONITORING EKRANI İÇİN:
http://localhost:5555/dashboard

RABBİT MANAGEMENT EKRANI İÇİN AŞAĞIDAKİ KOMUTLARI TERMİNALDE ÇALIŞTIRIN VE ARDINDAN ŞURAYA GİDİN http://localhost:15672/
- docker exec rabbitmq-node1 rabbitmq-plugins enable rabbitmq_management
- docker exec rabbitmq-node2 rabbitmq-plugins enable rabbitmq_management
- docker exec rabbitmq-node3 rabbitmq-plugins enable rabbitmq_management



TEKNİK MİMARİ:
- Sistemde kulalnlan teknolojiler:
    - Rabbitmq Cluster (3 replica ve önüne bir load balancer(Haproxy) olacak şekilde düşündüm, o yüzden 3 rabbit conteyneri ayağa kaldırdım bir rabit conteyneri düşse, diğeri yerine devam edecek)
    - Redis
    - Mongodb
    - Docker
    - Flask (Rest api)
    - Python
    - Celery

- Sistem çalışma mantığı: Aynı proje klasörü içinde "parser" ve "rest-api" adında 2 farklı proje bulunur. "parser" bitexen apiden datayı alıp db ye yazar ve db ye
yazdığı bu veriler üzerinden istatistik hesaplamalarını yapıp, ilgili mongodb collectionuna yazar. docker-compose üzerindeki "beat_move_data_to_db" ve "beat_calculate_statistics"
adlı servisler "parser" üzerinde çalışır. parser'in configleri parser/config/prod.yaml, rest-api'nin rest-api/config/prod.conf dosyalarında yer alır.
Cronjob gibi çalışan "beat_move_data_to_db" ve "beat_calculate_statistics" adlı servislerin kaçar saniyede bir çalışacağı bilgisi parser/config/prod.yaml adlı dosya içindedir.
Bir transactionu mongodb'ye yazarken aynı transactionun db ye iki kez yazılmasını engellemek için gelen transaction datasını hash'leyip redise "transaction_hash" adında bir key
ile yazıyorum ve bu keye 86400 sn yani 1 günlük bir expire süresi veriyorum ve daha sonra bitexen apiden bana yeni gelen dataları da hashleyip rediste varmı bu hash
diye kontrol ederek, eğer yoksa mongoya insert ediyorum. Bu kontrolü mongoda yapmak yerine rediste yapmamın nedeni tamamen performans, bu kontrolü sürekli insert alan bir
mongodb'den yapıp diski kontrol etmek yerine, ram de çalışan rediste kontrol etmek çok daha iyi olur diye düşündüm. "beat_calculate_statistics" servisi 1 dakikada bir çalışıp
420 adet satırı mongodaki "last_transactions" adlı collectiondan alır, gerekli hesaplamaları yapıp hesapladığı istatistikleri "statistics" adlı collectiona yazar ve yazdıktan
hemen sonra hesapladığı bu satırları "last_transactions" adlı collectiondan siler ve böylelikle "last_transactions" adlı collectionsta data birikmemiş ve tablo şişmemiş olur ki bu da performansı
artıracaktır. "beat_move_data_to_db" ve  "beat_calculate_statistics" adlı servisler 1 er concurrency ile çalışacak şekilde docker-compose üzerinden ayarlanmışlardır. Bu servislerin
çalışma durumlarını flower üzerinden şu adresten http://localhost:5555/dashboard takip edebilirsiniz .

İstatistikler:
    - günlükler için her güne 1 satır
    - haftalıklar için her haftaya 1 satır
    - aylıklar için her aya bir satır
olacak şekilde "statistics" adlı mongodb collectionunda tutulmaktadır.


İstatistik satırlarında unique'liği "statistics" adlı collections'da bulunan şu 3 field ile sağlıyorum:
    - stat_period
    - stat_type
    - date_key
 date_key field'ı:
    - Eğer istatistik satırının periyodu daily ise bu alanın değeri current_year|current_month|current_week|current_day olacak şekilde. örn; 2021|7|26|4
    - Eğer istatistik satırının periyodu weekly ise bu alanın değeri current_year|current_month|current_week olacak şekilde. örn; 2021|7|26
    - Eğer istatistik satırının periyodu monthly ise bu alanın değeri current_year|current_month olacak şekilde. örn; 2021|7



