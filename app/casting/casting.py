from dataclasses import dataclass


@dataclass
class Casting:
    id: int
    name: str
    original_name: str
    character: str
    profile_img_path: str
    gender: int
    department: str

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.original_name = kwargs.get('original_name')
        self.character = kwargs.get('character')
        self.profile_img_path = kwargs.get('profile_path')
        self.gender = kwargs.get('gender')
        self.department = kwargs.get('known_for_department')

    @property
    def is_an_actor(self) -> bool:
        return self.department == 'Acting'

    @property
    def is_female(self) -> bool:
        return self.gender == 1

    @property
    def is_male(self) -> bool:
        return not self.is_female
