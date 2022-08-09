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
                LineChartView(data: [1,2,1,5,2,5,7,3,2,7], title: "Apple",legend: "AAPL")
            }
        }
    }
}

class ControllerHoster: UIHostingController<SwiftUIView> {
    required init?(coder aDecoder: NSCoder) {
        super .init(coder: aDecoder, rootView: SwiftUIView())
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
}
