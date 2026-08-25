from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    manufacturer: str | None = None
    description: str | None = None
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


class ProductResponse(BaseModel):
    #build this schema from object attributes.
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    manufacturer: str | None = None
    description: str | None
    price: float
    stock: int

class ProductUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    manufacturer: str | None = None#can ignore to send manufacturer in json
    price: float = Field(gt=0)# grater than 0
    stock: int = Field(ge=0)#it is required, because you haven't given it a default value.

class ProductPatch(BaseModel):#an ignore to send all in json, because you haven't given it a default value.
    name: str | None = Field(default=None, min_length=2, max_length=200)
    manufacturer: str | None = None # str | None -> allowed types string OR None ---  = None -> default is None
    price: float | None = Field(default=None, gt=0)#can ignore to send it in json
    stock: int | None = Field(default=None, ge=0)    

class SemanticSearchResponse(BaseModel):
    product: ProductResponse
    similarity: float
