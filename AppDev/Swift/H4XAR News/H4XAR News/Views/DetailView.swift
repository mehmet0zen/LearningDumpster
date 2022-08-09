//
//  DetailView.swift
//  H4XAR News
//
//  Created by Mehmet Yusuf Ozen on 10/5/21.
//

import SwiftUI

struct DetailView: View {
    
    let url: String?
    
    var body: some View {
        WebView(urlString: url)
    }
}

struct DetailView_Previews: PreviewProvider {
    static var previews: some View {
        DetailView(url: "https:www.google.com")
    }
}

