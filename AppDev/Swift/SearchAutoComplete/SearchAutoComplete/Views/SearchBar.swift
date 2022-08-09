//
//  SearchBar.swift
//  SearchAutoComplete
//
//  Created by Mehmet Yusuf Ozen on 10/4/21.
//

import SwiftUI

struct SearchBar: View {
    
    let keyword: [String];
    @State var searchText : String;
    @State var isSearching : Bool;
    
    var body: some View {
        ScrollView {
            
            //Create SearchBar
            HStack {
                HStack{
                    Image(systemName: "magnifyingglass")
                    TextField("Search stocks...", text: $searchText)
                    
                    if !searchText.isEmpty {
                        Button(action: { searchText = "" }, label: {
                            Image(systemName: "xmark.circle.fill")
                                .font(.system(size: 20))
                        })
                    }
                }
                .padding(13)
                .background(Color(.systemGray6))
                .foregroundColor(Color(.systemGray2))
                .cornerRadius(12)
                .padding(.horizontal)
                .onTapGesture (perform: {
                    isSearching = true
                })
                .padding(.bottom, 12)
                .padding(.top, 12)
                .transition(.move(edge: .trailing))
                .animation(.spring())
                
                //If the user pressed search bar
                if isSearching {
                    //show the cancel button
                    Button (action: {
                        isSearching = false
                        searchText = ""
                        UIApplication.shared.endEditing(true)
                    }, label: {Text("Cancel")})
                        .padding(.trailing, 24)
                        .transition(.move(edge: .trailing))
                        .animation(.spring())
                        .foregroundColor(Color("darkModedText"))
                }
            }//HStack
            
            //add items with foreach loop
            if !searchText.isEmpty {
                ForEach((keyword).filter( {
                    "\($0)".starts(with: searchText)} ), id: \.self) { keywords in
                        //Stack items to seperate them
                        HStack {
                            NavigationLink(destination: ContentView()) {
                                Image(systemName: "magnifyingglass.circle.fill").foregroundColor(Color(.systemGray)).font(.system(size: 22))
                                Text("\(keywords)").foregroundColor(Color("darkModedText")).bold()
                            }
                            
                            Spacer()
                        }
                        .padding() //add padding
                        Divider() //add a line between items
                            .padding(.leading)
                            .background(Color(.systemGray6))
                    }//Foreach closed
            }
        }//ScrollView closed
        .resignKeyboardOnDragGesture()
        .navigationBarHidden(isSearching).animation(.default)
    }
}
struct SearchBar_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
        SearchBar(keyword: ["Hi","Hello","Whatsup"], searchText: "", isSearching: false)
                .navigationBarTitle("Title")
        }
            .previewLayout(.sizeThatFits)
            
    }
}

extension UIApplication {
    func endEditing(_ force: Bool) {
        self.windows
            .filter{$0.isKeyWindow}
            .first?
            .endEditing(force)
    }
}

struct ResignKeyboardOnDragGesture: ViewModifier {
    var gesture = DragGesture().onChanged{_ in
        UIApplication.shared.endEditing(true)
    }
    func body(content: Content) -> some View {
        content.gesture(gesture)
    }
}

extension View {
    func resignKeyboardOnDragGesture() -> some View {
        return modifier(ResignKeyboardOnDragGesture())
    }
}
