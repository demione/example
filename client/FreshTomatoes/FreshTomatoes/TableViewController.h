//
//  TableViewController.h
//  FreshTomatoes
//
//  Created by Demi on 5/11/16.
//  Copyright © 2016 Demiforce. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface TableViewController : UITableViewController

@property (nonatomic, weak) IBOutlet UISearchController *searchController;
@property (nonatomic, weak) IBOutlet UISearchBar *searchBar;

@end
