import pymongo
from bson import ObjectId, BSON, decode_all
from pymongo import MongoClient

DEFAULT_LIMIT = 1000


class MongodbHelper:
    def __init__(self, collection_name: str, db_dsn: str, db_name: str, username: str, password: str):
        try:
            self.collection_name = collection_name
            self.db_name = db_name
            self.db_dsn = db_dsn
            self.client = MongoClient(self.db_dsn)
            self.client.admin.authenticate(username, password)
            self.db = self.client[self.db_name]

        except Exception as ex:
            raise ex

    """def create_connection(self):
        client = MongoClient(self.db_uri)
        return client[self.db_name]"""

    def max_item(self, predicate: object = dict, sort: str = "_id"):
        return self.get_collection().find(predicate).sort({sort: -1})

    def get_collection(self):
        return self.db[self.collection_name]

    def distinct(self, key: str, predicate: object = dict) -> list:
        result = self.get_collection().distinct(key, predicate)
        return result

    def get_included_collection_names(self):
        return self.db.collection_names(include_system_collections=False)

    def add(self, entity: object) -> object:
        result = self.get_collection().insert_one(entity)
        return result.inserted_id

    def add_range(self, entities: list) -> list:
        result = self.get_collection().insert_many(entities)
        return result.inserted_ids

    # TODO: Methodun ismi değişecek
    def add_range2(self, entities: list, ordered: bool = True) -> list:
        result = self.get_collection().insert_many(entities, ordered=ordered)
        return result

    def get_single(self, predicate: object) -> object:
        result = self.get_collection().find_one(predicate)
        return result

    def get_single_with_fields(self, predicate: object, fields: object) -> object:
        result = self.get_collection().find_one(predicate, fields)
        return result

    def get_single_by_id(self, _id) -> object:
        result = self._get_single({"_id": ObjectId(_id), })
        return result

    def get_all(self, predicate={}, fields={}, get_all_fields: bool = False, sort: str = None, limit: int = None,
                skip: int = None) -> object:

        if get_all_fields:
            fields = None

        result = self.get_collection().find(predicate, fields)

        if skip is not None:
            result = result.skip(skip)

        if limit is not None:
            result = result.limit(limit)

        if sort is not None:
            result = result.sort(sort, -1)

        return result

    def aggregate(self, match: dict = dict, group: dict = dict):
        """
            {
                "$unwind": "$incoming"
            },
            {
                "$match": {
                    "$and": [{"hour": {"$gte": 11}}, {"hour": {"$lte": 12}}]
                }
            },
            {
                "$group": {
                    "_id": None,
                    "sum": {"$sum": "$incoming"}
                }
            }
        """

        return self.get_collection().aggregate(
            [
                {
                    "$match": match
                },
                {
                    "$group": group
                }
            ]
        )

    def count(self, predicate: dict = None) -> int:
        if predicate is None:
            return self.get_collection().count()
        else:
            return self.get_collection().find(predicate).count()

    def create_index(self, field_name: str, is_unique: bool = False):
        self.get_collection().create_index([(field_name, pymongo.ASCENDING)], unique=is_unique)

    def create_index_text_2(self, field_name: str):
        self.get_collection().ensure_index([
            (field_name, 'text'),
        ],
            name=field_name + "_index",
            # weights={
            #    field_name: weight,
            # }
        )

    def create_index_text(self, field_names: list):
        indexes = {}

        for i in field_names:
            indexes[i] = "text"

        self.get_collection().create_index(indexes)

    def get_index_names(self) -> sorted:
        result = self.get_collection().index_information()
        return sorted(list(result))

    def remove(self, predicate: dict) -> int:
        result = self.get_collection().delete_one(predicate)
        return result.deleted_count

    def remove_range(self, predicate: dict) -> int:
        result = self.get_collection().delete_many(predicate)
        return result.deleted_count

    def edit(self, predicate: dict, value: dict, is_upsert: bool = False) -> dict:
        """ UpdateOne({'_id': 4}, {'$inc': {'j': 1}}, upsert=True) """
        result = self.get_collection().update_one(predicate, {'$set': value}, upsert=is_upsert)
        return dict(
            matched_count=result.matched_count,
            modified_count=result.modified_count,
            upserted_id=result.upserted_id
        )

    def edit_for_array(self, predicate: dict, value: dict, is_upsert: bool = False) -> dict:
        """ UpdateOne({'_id': 4}, {'$inc': {'j': 1}}, upsert=True) """
        result = self.get_collection().update_one(predicate, value, upsert=is_upsert)
        return dict(
            matched_count=result.matched_count,
            modified_count=result.modified_count,
            upserted_id=result.upserted_id
        )

    def edit_range(self, predicate: dict, value: dict, is_upsert: bool = False) -> dict:
        """ UpdateMany({'_id': 4}, {'$inc': {'j': 1}}, upsert=True) """
        result = self.get_collection().update_many(predicate, {'$set': value}, upsert=is_upsert)
        return dict(
            matched_count=result.matched_count,
            modified_count=result.modified_count,
            upserted_id=result.upserted_id
        )

    def edit_range_for_array(self, predicate: dict, value: dict, is_upsert: bool = False) -> dict:
        """ UpdateMany({'_id': 4}, {'$inc': {'j': 1}}, upsert=True) """
        result = self.get_collection().update_many(predicate, value, upsert=is_upsert)
        return dict(
            matched_count=result.matched_count,
            modified_count=result.modified_count,
            upserted_id=result.upserted_id
        )

    def replace(self, predicate: dict, value: dict, is_upsert: bool = False) -> dict:
        """ ReplaceOne({'j': 1}, {'j': 2})]) """
        result = self.get_collection().replace_one(predicate, value, upsert=is_upsert)
        return dict(
            matched_count=result.matched_count,
            modified_count=result.modified_count,
            upserted_id=result.upserted_id
        )

    ''' https://stackoverflow.com/questions/39606506/using-a-generator-to-iterate-over-a-large-collection-in-mongo '''

    def batch_iterator(self, predicate, fields: object = dict, limit=DEFAULT_LIMIT, skip=0, sort=None,
                       no_cursor_timeout: bool = False, sort_type: int = -1):

        while True:
            results = self.get_collection().find(predicate, fields, no_cursor_timeout=no_cursor_timeout)

            if sort is not None:
                # print("sort")
                results = results.sort(sort, sort_type)

            if limit is not None:
                # print("limit")
                results = results.limit(limit)

            if skip is not None:
                # print("skip")
                results = results.skip(skip)

            try:
                results.next()

            except StopIteration:
                break

            for result in results:
                yield result

            skip += limit

        '''
        ref_results_iter = self.mongo_iterator(cursor=latest_rents_refs, limit=50000)
        for ref in ref_results_iter:
            results_latest1.append(ref)
        '''

    def dump(self, file_path):
        if not file_path:
            raise Exception("file_path not found", "file_path")

        with open(file_path, 'wb+') as f:
            for doc in self.get_collection().find():
                f.write(BSON.encode(doc))

    def restore(self, file_path):
        if not file_path:
            raise Exception("file_path not found", "file_path")

        with open(file_path, 'rb') as f:
            self.get_collection().insert(decode_all(f.read()))

    def add_to_set(self, predicate: dict, value: dict, is_upsert: bool = False) -> dict:
        """ UpdateOne({'_id': 4}, {'$inc': {'j': 1}}, upsert=True) """
        result = self.get_collection().update_one(predicate, {'$addToSet': value}, upsert=is_upsert)
        return dict(
            matched_count=result.matched_count,
            modified_count=result.modified_count,
            upserted_id=result.upserted_id
        )