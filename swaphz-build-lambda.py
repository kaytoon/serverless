import boto3
import StringIO
import zipfile
import mimetypes
def lambda_handler(event, context):
    s3 = boto3.resource('s3')

    swaphz_bucket = s3.Bucket('swaphz')
    build_bucket = s3.Bucket('build-swaphz')

    swaphz_zip = StringIO.StringIO()  
    build_bucket.download_fileobj('swaphzbuild.zip', swaphz_zip)  

    with zipfile.ZipFile(swaphz_zip) as myzip:  
        for nm in myzip.namelist():  
            obj = myzip.open(nm)
            swaphz_bucket.upload_fileobj(obj,nm,ExtraArgs ={'ContentType': mimetypes.guess_type(nm)[0]})
            swaphz_bucket.Object(nm).Acl().put(ACL='public-read')
    return 'Hello from Lambda'
