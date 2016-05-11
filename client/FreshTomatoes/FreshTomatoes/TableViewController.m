//
//  TableViewController.m
//  FreshTomatoes
//
//  Created by Demi on 5/11/16.
//  Copyright © 2016 Demiforce. All rights reserved.
//

#import "TableViewController.h"
#import "DetailViewController.h"
#import "MovieTableViewCell.h"
#import "Movie.h"
#import "UIImageView+AFNetworking.h"

@interface TableViewController ()

@property (nonatomic) NSMutableArray<Movie *> *movies;
@property (nonatomic) NSArray *searchResults;

@end

@implementation TableViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    self.title = @"Fresh Tomatoes";

    [self downloadMoviesJson];
    
    // Uncomment the following line to preserve selection between presentations.
    // self.clearsSelectionOnViewWillAppear = NO;
    
    // Uncomment the following line to display an Edit button in the navigation bar for this view controller.
    // self.navigationItem.rightBarButtonItem = self.editButtonItem;
}

- (void) downloadMoviesJson {
    NSMutableURLRequest *request =
    [NSMutableURLRequest requestWithURL:[NSURL
                                         URLWithString:@"http://localhost:8080/movies"]
                            cachePolicy:NSURLRequestReloadIgnoringLocalAndRemoteCacheData
                        timeoutInterval:10
     ];
    
    [request setHTTPMethod: @"GET"];
    
    NSURLSession *session = [NSURLSession sessionWithConfiguration:[NSURLSessionConfiguration defaultSessionConfiguration]];
    
    [[session dataTaskWithRequest:request
                completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
                    
                    if (data && error == nil) {
                        NSArray *jsonData = [NSJSONSerialization
                                                  JSONObjectWithData:data
                                                  options:NSJSONReadingMutableContainers
                                                  error:&error];
                        
                        [self performSelectorOnMainThread:@selector(loadJsonData:) withObject:jsonData waitUntilDone:NO];
                    }
                    
                }] resume];
}

- (void) loadJsonData: (id) obj {
    if (obj) {
        NSArray *jsonData = (NSArray *)obj;
        self.movies = [[NSMutableArray alloc] initWithCapacity:jsonData.count];
        for (NSDictionary *movieDict in jsonData) {
            Movie *movie = [[Movie alloc] init];
            movie.name = movieDict[@"movie_name"];
            movie.thumbnailURL = movieDict[@"image_url"];
            movie.rating = [movieDict[@"rating"] floatValue];
            movie.movieDescription = movieDict[@"description"];
            [self.movies addObject:movie];
        }
        [self.tableView reloadData];
    }
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - Table view data source

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView {
    return 1;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    if (self.searchResults.count) {
        return [self.searchResults count];
        
    } else {
        return (self.movies ? self.movies.count : 0);
    }
}

-(void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath
{
    [self performSegueWithIdentifier:@"detailSegue" sender:self];
}

- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    if ([[segue identifier] isEqualToString:@"detailSegue"])
    {
        NSIndexPath *indexPath = [self.tableView indexPathForSelectedRow];
        if (indexPath) {
            if (segue.destinationViewController) {
                DetailViewController *detailController = (DetailViewController *)segue.destinationViewController;
                detailController.movie = [self.movies objectAtIndex:indexPath.row];
            }
        }
    }
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
    static NSString *movieTableIdentifier = @"MovieTableItem";
    
    MovieTableViewCell *cell = [self.tableView dequeueReusableCellWithIdentifier:movieTableIdentifier];
    
    if (cell == nil) {
        NSArray *nib = [[NSBundle mainBundle] loadNibNamed:@"MovieTableViewCell" owner:self options:nil];
        cell = [nib objectAtIndex:0];
    }
    
    Movie *movie = nil;
    if (self.searchResults && indexPath.row < self.searchResults.count) {
        movie = [self.searchResults objectAtIndex:indexPath.row];
    } else {
        movie = [self.movies objectAtIndex:indexPath.row];
    }
    
    [cell.thumbnailImageView setImageWithURL:[NSURL URLWithString:movie.thumbnailURL] placeholderImage:[UIImage imageNamed:@"placeholder.png"]];
    cell.nameLabel.text = movie.name;
    cell.ratingLabel.text = [NSString stringWithFormat:@"Rating: %.01f/5 stars", movie.rating];
    cell.descriptionLabel.text = movie.movieDescription;
    
    return cell;
}

- (CGFloat)tableView:(UITableView *)tableView heightForRowAtIndexPath:(NSIndexPath *)indexPath
{
    return 78.;
}

- (void)filterContentForSearchText:(NSString*)searchText scope:(NSString*)scope
{
    NSPredicate *resultPredicate = [NSPredicate
                                    predicateWithFormat:@"name contains[cd] %@",
                                    searchText];
    
    if (self.movies) {
        self.searchResults = [self.movies filteredArrayUsingPredicate:resultPredicate];
    }
}

-(BOOL)searchDisplayController:(UISearchController *)controller shouldReloadTableForSearchString:(NSString *)searchString
{
    [self filterContentForSearchText:searchString
                               scope:[[self.searchBar scopeButtonTitles]
                                      objectAtIndex:[controller.searchBar
                                                     selectedScopeButtonIndex]]];
    
    return YES;
}

@end
