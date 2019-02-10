import requests
from mamba import *
from expects import *


with description('api') as self:
    with it('is up and running'):
        response = requests.get(url='http://localhost:3000/')

        expect(response.text).to(equal('Hello, World!'))
