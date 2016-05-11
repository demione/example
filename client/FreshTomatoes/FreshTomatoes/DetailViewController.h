//
//  DetailViewController.h
//  FreshTomatoes
//
//  Created by Demi on 5/11/16.
//  Copyright © 2016 Demiforce. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "Movie.h"

@interface DetailViewController : UIViewController

@property (nonatomic) Movie *movie;
@property (nonatomic, weak) IBOutlet UILabel *nameLabel;
@property (nonatomic, weak) IBOutlet UILabel *ratingLabel;
@property (nonatomic, weak) IBOutlet UIImageView *thumbnailImageView;
@property (nonatomic, weak) IBOutlet UILabel *descriptionLabel;

@end
