//
//  ContentView.swift
//  SearchAutoComplete
//
//  Created by Mehmet Yusuf Ozen on 10/3/21.
//

import SwiftUI

struct ContentView: View {
    
    @State var searchText = "";
    @State var isSearching = false;
    var keyword = ["AAPL","AMZN","MSFT","NVDA","NFLX","GOOGL","DIS","GOOG","FDX"];
    
    var body: some View {
        NavigationView {
            //Create a body navigation for searched items
            ScrollView(.vertical, showsIndicators: false) {
                SearchBar_iOS15(keyword: keyword, searchText: searchText, isSearching: isSearching)
            }
            .padding(.horizontal, 3)
            //add title
            .navigationBarTitle("Skyrocket 🚀", displayMode: .large)
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
        ContentView()
            .colorScheme(.dark)
    }
}
