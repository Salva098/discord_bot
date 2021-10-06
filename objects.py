
class users:
    def __init__(self,id,num_user,level,exp,exp_max):
        self.id=id
        self.num_user=num_user
        self.level=level
        self.exp=exp
        self.exp_max=exp_max
    def __str__(self) -> str:
        return "la id "+ str(self.id) + " con el numero "+str(self.num_user)+", nivel : "+ str(self.level)+", experiencia: "+str(self.exp)+ ", siguiente niviel: " +str(self.exp_max)


class Game:
    def __init__(self,title,worth,image,description,instructions,open_giveaway_url,type,plataforms,published_date,end_date):
        self.title = title
        self.worth = worth
        self.image = image
        self.description = description
        self.instructions = instructions
        self.open_giveaway_url = open_giveaway_url
        self.type = type
        self.published_date=published_date
        self.plataforms = plataforms
        self.end_date = end_date