//
//  WeatherModel.swift
//  Clima
//
//  Created by Mehmet Yusuf Ozen on 8/6/21.
//  Copyright © 2021 App Brewery. All rights reserved.
//

import Foundation

struct WeatherModel {
    let conditionId: Int
    let cityName: String
    let temperature: Double
    
    var tempString: String {
        return String(format: "%.1f", temperature)
    }
    
    var conditionName: String {
        switch conditionId {
            case 200...202:
                return "cloud.bolt.rain"
            case 210...232:
                return "cloud.bolt"
            case 300...321:
                return "cloud.drizzle"
            case 500...501:
                return "cloud.rain"
            case 502...511:
                return "cloud.heavyrain"
            case 520...531:
                return "cloud.rain"
            case 600...622:
                return "cloud.snow"
            case 701...781:
                return "cloud.fog"
            case 800:
                return "sun.max"
            case 801...804:
                return "cloud.bolt"
            default:
                return "cloud"
        }
    }
    
    func getTemperatur(temp: Double) -> Double {
        return temp
    }
    func getDescription(desc: String) -> String {
        return desc
    }
}
