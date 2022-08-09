//
//  ResultsController.swift
//  CryptoCalculator
//
//  Created by Mehmet Yusuf Ozen on 8/15/21.
//

import UIKit

class ResultsController: UIViewController {
    
    @IBOutlet weak var resultLabel: UILabel!
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    @IBAction func recalculatePressed(_ sender: UIButton) {
        self.dismiss(animated: true, completion: nil)
    }
}
