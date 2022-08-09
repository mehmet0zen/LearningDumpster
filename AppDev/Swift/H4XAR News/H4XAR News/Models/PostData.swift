//
//  PostData.swift
//  H4XAR News
//
//  Created by Mehmet Yusuf Ozen on 10/5/21.
//

import Foundation

struct Results: Decodable {
    let hits: [Post]
    
}

struct Post: Decodable, Identifiable {
    var id: String {
        return objectID
    }
    let objectID: String
    let points: Int
    let title: String
    let url: String?
}
