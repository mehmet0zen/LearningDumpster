//
//  SwiftUIView.swift
//  TestStoryBoardChart
//
//  Created by Mehmet Yusuf Ozen on 11/7/21.
//

import SwiftUI
import SwiftUICharts

struct SwiftUIView: View {
    var body: some View {
        VStack {
            HStack {
                Image("apple_logo")
                        .padding()
                        .frame(width: 220.0, height: 220.0)
                        .controlSize(.mini).cornerRadius(25)
                        .shadow(color: .gray, radius: 10, x: 0.5, y: 0.5)
            }
        }
    }
}

class HostingController: UIHostingController<SwiftUIView> {
    required init?(coder: NSCoder) {
        super.init(coder: coder, rootView: SwiftUIView());
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
}
