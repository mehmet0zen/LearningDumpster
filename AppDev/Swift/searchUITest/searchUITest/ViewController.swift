//
//  ViewController.swift
//  searchUITest
//
//  Created by Mehmet Yusuf Ozen on 10/3/21.
//

import UIKit

class ViewController: UIViewController, UISearchResultsUpdating, UISearchBarDelegate {

    //Set search controller as UISearchController
    let searchController = UISearchController()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        title = "Skyrocket 🚀"
        //SEARCH CONTROLLER
        searchController.searchBar.delegate = self
        searchController.searchResultsUpdater = self
        navigationItem.searchController = searchController
    }

    func updateSearchResults(for searchController: UISearchController) {
        guard let text = searchController.searchBar.text else {
            return
        }
        
        print(text)
    }
}

