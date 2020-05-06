# crossReference

python utility to crossreference Letterboxd watchlist with libraries of preferred streaming services

The user's Letterboxd username is used to scrape their Letterboxd watchlist with requests + BeautifulSoup. 
The user's country is requested from [ipinfo.io](https://ipinfo.io), and used to generate a list of all available streaming services using [JustWatch](https://justwatch.com).
The user types each streaming service they would like to reference, and these inputs are verified with the list of available services, using get_close_matches() to prompt the user on mis- or close spellings. 
The user will then review the full list of services and be able to add or remove any/all of them before the 
Each film is then searched with JustWatch and stored with every service in the user's preferences that it is available on. 

On subsequent runs of the script, the user can either pass -r as a flag to reconfigure the entire setup. If this option is not selected, the script will use their previous configuration of username and preferred services, but will always update their wishlist. 

## usage

On install, chmod +x-ing and running the crossRef.py script will configure your watchlist based on your Letterboxd username, accept and validate your preferred streaming services, and then print out which films from the watchlist are available on each service.    

## Note

This project uses the [unoffical Justwatch API](https://github.com/dawoudt/JustWatchAPI) developed by [dawoudt](https://github.com/dawoudt). as such, this cannot be incorporated into any commercial or otherwise high volume projects. 

feel free to [add me on Letterboxd!](https://letterboxd.com/cmurph29/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
