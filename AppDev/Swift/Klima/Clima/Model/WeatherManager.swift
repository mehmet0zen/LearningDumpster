//
//  WeatherManager.swift
//  Clima
//
//  Created by Mehmet Yusuf Ozen on 8/4/21.
//  Copyright © 2021 App Brewery. All rights reserved.
//

import Foundation
import MapKit

protocol WeatherManagerDelegate {
    func didUpdateWeather(_ weatherManager: WeatherManager, weather: WeatherModel)
    func didFailWithError(_ error: Error)
}

struct WeatherManager {
    let weatherURL = "https://api.openweathermap.org/data/2.5/weather?appid=cf1f71c838f65527a0668ae48bc9b395&units=metric"
    
    var delegate: WeatherManagerDelegate?
    
    
    func performRequest(with urlString: String) {
        //create url
        if let url = URL(string: urlString) {
            //create url session
            let session = URLSession(configuration: .default)
            
            //create task
            let task = session.dataTask(with: url) { (data, response, error) in
                if error != nil {
                    delegate?.didFailWithError(error!)
                    return
                }
                if let safeData = data {
                    if let weather = self.parseJSON(safeData) {
                        self.delegate?.didUpdateWeather(self, weather: weather)
                    }
                }
            }
            
            //start task
            task.resume()
        }
    }
    func parseJSON(_ weatherData: Data) -> WeatherModel? {
        let decoder = JSONDecoder()
        do {
            let decodedData = try decoder.decode(WeatherData.self, from: weatherData)
            //API DATA
            let name = decodedData.name
            let temp = decodedData.main.temp
            let id = decodedData.weather[0].id
            //let description = decodedData.weather[0].description
            
            let weather = WeatherModel(conditionId: id, cityName: name, temperature: temp)
            
            return weather
        } catch {
            delegate?.didFailWithError(error)
            return nil
        }
    }
}

//MARK: - WeatherManagerExtension
extension WeatherManager {
    func fetchWeather(latitude: CLLocationDegrees, longitude: CLLocationDegrees) {
        let urlString = "\(weatherURL)&lat=\(latitude)&lon=\(longitude)"
        performRequest(with: urlString)
    }
    
    func fetchWeather(cityName: String) {
        let urlString = "\(weatherURL)&q=\(cityName)"
        performRequest(with: urlString)
    }
}
