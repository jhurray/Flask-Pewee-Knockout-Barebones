from datetime import datetime

class CacheObject:

  def __init__(self, value, timeout=None):
    self.timeout = timeout
    self.lastReferenced = datetime.now()
    self.value = value

class Cache:

  def __init__(self):
    self.data = dict()

  def __del__(self):
    print "deleting cache..."
    for key in self.data:
      cacheObject = self.data.pop(key)
      del cacheObject
  
  def has(self, key):
    if key in self.data and self.shouldRefresh(self.data[key]):
      self.remove(key)
    return key in self.data

  def get(self, key):
    if self.has(key):
      cacheObject = self.data[key]
      cacheObject.lastReferenced = datetime.now()
      return cacheObject.value
    else:
      raise Exception('Key does not exist in cache... maybe it timed out!')

  def put(self, key, value=None, timeout=30):
    newCacheObject = CacheObject(value, timeout)
    self.data[key] = newCacheObject
      
  def remove(self, key):
    self.data.pop(key)

  def shouldRefresh(self, cacheObject):
    delta = datetime.now() - cacheObject.lastReferenced
    if delta.seconds >= cacheObject.timeout*60: # every *timeout* mins
      return True
    else:
      return False


#############################  SETUP  #####################################

''' GLOBAL '''
cache = Cache()



