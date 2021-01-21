import abc

class AbstractRepository(abc.ABC):
	@abc.abstractmethod
	def query(self):
		raise NotImplementedError

	@abc.abstractmethod
	def add(self):
		raise NotImplementedError
		
	@abc.abstractmethod
	def update(self):
		raise NotImplementedError

	@abc.abstractmethod
	def delete(self):
		raise NotImplementedError

	@abc.abstractmethod
	def commit(self):
		raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
	def __init__(self,session):
		self.session = session

	def query(self,inquiry):
		return self.session.query(inquiry).all()
		
	def add(self,additive):
		self.session.add(additive)
		
	def update(self,model,updatum):
		self.session.query(model).update(updatum)
		
	def delete(self,model):
		self.session.query(model).delete()
		
	def commit(self):
		self.session.commit()