//
//  SearchBar-iOS15.swift
//  SearchAutoComplete
//
//  Created by Mehmet Yusuf Ozen on 10/6/21.
//

import SwiftUI

struct SearchBar_iOS15: View {
    let keyword: [String];
    @State var searchText : String;
    @State var isSearching : Bool;
    
    var body: some View {
        if #available(iOS 15.0, *) {
            ScrollView {
                
                //add items with foreach loop
                if !searchText.isEmpty {
                    ForEach((keyword).filter( { "\($0)".starts(with: searchText)} ), id: \.self) { keywords in
                            //Stack items to seperate them
                            HStack {
                                NavigationLink(destination: ContentView()) {
                                    Image(systemName: "magnifyingglass.circle.fill").foregroundColor(Color(.systemGray)).font(.system(size: 22))
                                    Text("\(keywords)").foregroundColor(Color("darkModedText")).bold()
                                }
                                
                                Spacer()
                            }
                            .padding() //add padding
                            .transition(.move(edge: .leading))
                            .animation(.spring())
                            Divider() //add a line between items
                                .padding(.leading)
                                .background(Color(.systemGray6))
                    }//Foreach closed
                }
            }//ScrollView closed
            .searchable(text: $searchText, prompt: "Search stocks...")
        } else {
            SearchBar(keyword: keyword, searchText: searchText, isSearching: isSearching)
        }
    }
}

struct SearchBar_iOS15_Previews: PreviewProvider {
    static var previews: some View {
        SearchBar_iOS15(keyword: ["Hi","Hello","Whatsup"], searchText: "", isSearching: false)
            .previewLayout(.sizeThatFits)
    }
}
