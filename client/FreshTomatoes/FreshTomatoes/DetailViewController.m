//
//  DetailViewController.m
//  FreshTomatoes
//
//  Created by Demi on 5/11/16.
//  Copyright © 2016 Demiforce. All rights reserved.
//

#import "DetailViewController.h"
#import "UIImageView+AFNetworking.h"

@interface DetailViewController ()

@end

@implementation DetailViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    if (self.movie) {
        self.title = self.movie.name;
        [self.thumbnailImageView setImageWithURL:[NSURL URLWithString:self.movie.thumbnailURL] placeholderImage:[UIImage imageNamed:@"placeholder.png"]];
        self.nameLabel.text = self.movie.name;
        self.ratingLabel.text = [NSString stringWithFormat:@"Rating: %.01f/5 stars", self.movie.rating];
        self.descriptionLabel.text = self.movie.movieDescription;
    }
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

/*
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}
*/

@end
