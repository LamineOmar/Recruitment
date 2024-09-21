from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "Files_validate_successfully"
    FILE_TYPE_NOT_SUPPORTED = "Files_type_not_supported"
    FILE_SIZE_EXCEEDED = "Files_size_exceeded"
    FILE_UPLOAD_SUCCESS = "Files_upload_success"
    FILE_UPLOAD_FAILED = "Files_upload_failed"
    
    POST_VALIDATED_SUCCESS="Post_validate_successfully"
    POST_SIZE_EXCEEDED="Post_size_exceeded"
    POST_UPLOAD_SUCCESS = "Post_upload_success"
    POST_UPLOAD_FAILED = "Post_upload_failed"